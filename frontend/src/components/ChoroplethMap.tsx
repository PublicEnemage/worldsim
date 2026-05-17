import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { FeatureCollection } from "geojson";
import type { GeoJSONFeatureCollection, ChoroplethFeatureProperties } from "../types";

const API_BASE = "http://localhost:8000/api/v1";
const SOURCE_ID = "worldsim-choropleth";
const FILL_LAYER_ID = "choropleth-fill";
const LINE_LAYER_ID = "choropleth-line";
const MAP_STYLE = "https://demotiles.maplibre.org/style.json";

interface Props {
  attributeName: string;
  title: string;
  scenarioId?: string | null;
  currentStep?: number | null;
  onEntityClick?: (entityId: string) => void;
}

// INTENT: Compute five breakpoints [p0, p25, p50, p75, p100] from feature
//         attribute values for use as MapLibre step-expression thresholds.
// PRECONDITIONS: features is an array of GeoJSON features whose
//                properties.attribute_value can be parsed as a finite float;
//                features may be empty or contain non-finite values which
//                are filtered out before quantile computation.
// POSTCONDITIONS: Returns a five-element number array that is strictly
//                 ascending; the MapLibre step-expression invariant is always
//                 satisfied. Returns a dummy ascending sequence when features
//                 is empty or all values are identical.
// ERROR CASES: Collapsed quantiles (non-strictly-ascending raw percentiles,
//              common for ordinal attributes like economy_tier or income_group)
//              produce an equal-width fallback spanning [min, max] — correct
//              for rendering but does not preserve distribution density shape.
// KNOWN LIMITATIONS: Falls back to equal-width intervals for ordinal
//                    attributes where many countries share the same value —
//                    colour bands reflect value range, not population density.
//                    No unit test coverage; verified via Playwright E2E only.
// computeSteps returns five breakpoints [p0, p25, p50, p75, p100] used as
// MapLibre step-expression thresholds. MapLibre requires strictly ascending
// thresholds — duplicate values (collapsed quantiles) produce broken rendering.
//
// Collapsed quantiles occur for small-range ordinal attributes like economy_tier
// (1–7) or income_group (1–5) when many countries share the same tier value.
// In that case we fall back to evenly-spaced breakpoints across [min, max] so
// colour variation is always visible regardless of distribution shape.
function computeSteps(features: GeoJSONFeatureCollection["features"]): number[] {
  const values = features
    .map((f) => parseFloat(f.properties.attribute_value))
    .filter((v) => isFinite(v))
    .sort((a, b) => a - b);

  if (values.length === 0) return [0, 1, 2, 3, 4];

  const min = values[0];
  const max = values[values.length - 1];
  const range = max - min;

  // Degenerate case: all values identical — return a dummy span so the step
  // expression stays valid; the single-colour result is correct.
  if (range === 0) return [min, min + 1, min + 2, min + 3, min + 4];

  const pct = (p: number) => values[Math.floor((p / 100) * (values.length - 1))];
  const raw = [pct(0), pct(25), pct(50), pct(75), pct(100)];

  // If quantiles are not strictly ascending (collapsed distribution), fall back
  // to four equal-width intervals spanning [min, max]. This ensures each colour
  // band covers a distinct portion of the value range.
  const isStrictlyAscending = raw.every((v, i) => i === 0 || v > raw[i - 1]);
  if (!isStrictlyAscending) {
    const step = range / 4;
    return [min, min + step, min + 2 * step, min + 3 * step, max];
  }

  return raw;
}

export default function ChoroplethMap({ attributeName, title, scenarioId, currentStep, onEntityClick }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const popupRef = useRef<maplibregl.Popup | null>(null);
  const onEntityClickRef = useRef(onEntityClick);
  const [error, setError] = useState<string | null>(null);

  // Keep ref current so the map click handler always calls the latest prop
  onEntityClickRef.current = onEntityClick;

  // Initialise the map once
  useEffect(() => {
    if (!containerRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: MAP_STYLE,
      center: [0, 20],
      zoom: 1.5,
    });
    mapRef.current = map;

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Fetch and update choropleth data when attributeName changes
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    setError(null);

    const load = async () => {
      let url = `${API_BASE}/choropleth/${attributeName}`;
      if (scenarioId != null && currentStep != null) {
        url += `?scenario_id=${encodeURIComponent(scenarioId)}&step=${currentStep}`;
      }
      const res = await fetch(url);
      if (res.status === 404) {
        setError(`No data available for attribute "${attributeName}".`);
        return;
      }
      if (!res.ok) {
        setError(`API error ${res.status} fetching "${attributeName}".`);
        return;
      }

      const data: GeoJSONFeatureCollection = await res.json();
      const steps = computeSteps(data.features);

      const applyData = () => {
        // Remove existing layers/source if present from a prior attribute
        if (map.getLayer(FILL_LAYER_ID)) map.removeLayer(FILL_LAYER_ID);
        if (map.getLayer(LINE_LAYER_ID)) map.removeLayer(LINE_LAYER_ID);
        if (map.getSource(SOURCE_ID)) map.removeSource(SOURCE_ID);

        map.addSource(SOURCE_ID, { type: "geojson", data: data as unknown as FeatureCollection });

        // Fill layer — step expression, attribute_value converted via to-number
        map.addLayer({
          id: FILL_LAYER_ID,
          type: "fill",
          source: SOURCE_ID,
          paint: {
            "fill-color": [
              "step",
              ["to-number", ["get", "attribute_value"]],
              "#f7fbff",
              steps[1], "#bdd7e7",
              steps[2], "#6baed6",
              steps[3], "#2171b5",
              steps[4], "#08306b",
            ],
            "fill-opacity": 0.8,
          },
        });

        // Border layer
        map.addLayer({
          id: LINE_LAYER_ID,
          type: "line",
          source: SOURCE_ID,
          paint: {
            "line-color": "#333333",
            "line-opacity": 0.3,
            "line-width": 0.5,
          },
        });

        // Hover popup
        popupRef.current?.remove();
        const popup = new maplibregl.Popup({
          closeButton: false,
          closeOnClick: false,
        });
        popupRef.current = popup;

        map.on("mousemove", FILL_LAYER_ID, (e) => {
          if (!e.features?.length) return;
          // Only show pointer cursor when click will do something
          map.getCanvas().style.cursor = onEntityClickRef.current ? "pointer" : "";

          const props = e.features[0].properties as ChoroplethFeatureProperties;
          const noteHtml = props.has_territorial_note && props.territorial_note
            ? `<p style="font-style:italic;margin:4px 0 0;font-size:11px">${props.territorial_note}</p>`
            : "";

          popup
            .setLngLat(e.lngLat)
            .setHTML(
              `<strong>${props.name ?? props.entity_id}</strong>` +
              `<br/>${title}: ${props.attribute_value}` +
              `<br/>Confidence tier: ${props.confidence_tier ?? "—"}` +
              noteHtml
            )
            .addTo(map);
        });

        map.on("mouseleave", FILL_LAYER_ID, () => {
          map.getCanvas().style.cursor = "";
          popup.remove();
        });

        // Country click — fire onEntityClick if wired (ref avoids stale closure)
        map.on("click", FILL_LAYER_ID, (e) => {
          if (!e.features?.length || !onEntityClickRef.current) return;
          const props = e.features[0].properties as ChoroplethFeatureProperties;
          onEntityClickRef.current(props.entity_id);
        });
      };

      if (map.isStyleLoaded()) {
        applyData();
      } else {
        map.once("load", applyData);
      }
    };

    load().catch(() => {
      setError(`Failed to fetch data for "${attributeName}".`);
    });
  }, [attributeName, title, scenarioId, currentStep]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
      {error && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            background: "rgba(255,255,255,0.9)",
            padding: "16px 24px",
            borderRadius: 6,
            border: "1px solid #ccc",
            fontSize: 14,
          }}
        >
          {error}
        </div>
      )}
    </div>
  );
}

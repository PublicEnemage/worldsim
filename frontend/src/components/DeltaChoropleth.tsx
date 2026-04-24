import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import type { FeatureCollection } from "geojson";
import type { GeoJSONFeatureCollection, DeltaChoroplethFeatureProperties } from "../types";

const API_BASE = "http://localhost:8000/api/v1";
const SOURCE_ID = "worldsim-delta";
const FILL_LAYER_ID = "delta-fill";
const LINE_LAYER_ID = "delta-line";
const MAP_STYLE = "https://demotiles.maplibre.org/style.json";

interface Props {
  scenarioAId: string;
  scenarioBId: string;
  attributeName: string;
  title: string;
}

function computeDivergingSteps(features: GeoJSONFeatureCollection["features"]): {
  negSteps: number[];
  posSteps: number[];
} {
  const values = features
    .map((f) => parseFloat(f.properties.attribute_value as string))
    .filter((v) => isFinite(v));

  const negValues = values.filter((v) => v < 0).sort((a, b) => a - b);
  const posValues = values.filter((v) => v > 0).sort((a, b) => a - b);

  const pct = (arr: number[], p: number) =>
    arr[Math.floor((p / 100) * (arr.length - 1))];

  const negSteps =
    negValues.length > 0
      ? [pct(negValues, 0), pct(negValues, 33), pct(negValues, 66), pct(negValues, 100)]
      : [-4, -3, -2, -1];

  const posSteps =
    posValues.length > 0
      ? [pct(posValues, 0), pct(posValues, 33), pct(posValues, 66), pct(posValues, 100)]
      : [1, 2, 3, 4];

  return { negSteps, posSteps };
}

export default function DeltaChoropleth({
  scenarioAId,
  scenarioBId,
  attributeName,
  title,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const popupRef = useRef<maplibregl.Popup | null>(null);
  const [error, setError] = useState<string | null>(null);

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

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    setError(null);

    const load = async () => {
      const url =
        `${API_BASE}/choropleth/${attributeName}/delta` +
        `?scenario_a=${encodeURIComponent(scenarioAId)}` +
        `&scenario_b=${encodeURIComponent(scenarioBId)}`;

      const res = await fetch(url);
      if (res.status === 404) {
        setError(`No delta data for attribute "${attributeName}" across these scenarios.`);
        return;
      }
      if (!res.ok) {
        setError(`API error ${res.status} fetching delta for "${attributeName}".`);
        return;
      }

      const data: GeoJSONFeatureCollection = await res.json();
      const { negSteps, posSteps } = computeDivergingSteps(data.features);

      const applyData = () => {
        if (map.getLayer(FILL_LAYER_ID)) map.removeLayer(FILL_LAYER_ID);
        if (map.getLayer(LINE_LAYER_ID)) map.removeLayer(LINE_LAYER_ID);
        if (map.getSource(SOURCE_ID)) map.removeSource(SOURCE_ID);

        map.addSource(SOURCE_ID, { type: "geojson", data: data as unknown as FeatureCollection });

        // Diverging color scale: red (decrease) → white (unchanged) → blue (increase)
        map.addLayer({
          id: FILL_LAYER_ID,
          type: "fill",
          source: SOURCE_ID,
          paint: {
            "fill-color": [
              "step",
              ["to-number", ["get", "attribute_value"]],
              "#67001f",
              negSteps[1], "#d6604d",
              negSteps[2], "#fddbc7",
              negSteps[3], "#f7f7f7",
              0, "#f7f7f7",
              posSteps[0], "#d1e5f0",
              posSteps[1], "#4393c3",
              posSteps[2], "#2166ac",
              posSteps[3], "#053061",
            ],
            "fill-opacity": 0.8,
          },
        });

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

        popupRef.current?.remove();
        const popup = new maplibregl.Popup({
          closeButton: false,
          closeOnClick: false,
        });
        popupRef.current = popup;

        map.on("mousemove", FILL_LAYER_ID, (e) => {
          if (!e.features?.length) return;
          map.getCanvas().style.cursor = "pointer";

          const props = e.features[0].properties as DeltaChoroplethFeatureProperties;
          const noteHtml =
            props.has_territorial_note && props.territorial_note
              ? `<p style="font-style:italic;margin:4px 0 0;font-size:11px">${props.territorial_note}</p>`
              : "";
          const dirIcon =
            props.delta_direction === "increase"
              ? "▲"
              : props.delta_direction === "decrease"
              ? "▼"
              : "—";

          popup
            .setLngLat(e.lngLat)
            .setHTML(
              `<strong>${props.name ?? props.entity_id}</strong>` +
                `<br/>${title} (A): ${props.value_a}` +
                `<br/>${title} (B): ${props.value_b}` +
                `<br/>Delta: ${props.attribute_value} ${dirIcon}` +
                `<br/>Confidence tier: ${props.confidence_tier ?? "—"}` +
                noteHtml
            )
            .addTo(map);
        });

        map.on("mouseleave", FILL_LAYER_ID, () => {
          map.getCanvas().style.cursor = "";
          popup.remove();
        });
      };

      if (map.isStyleLoaded()) {
        applyData();
      } else {
        map.once("load", applyData);
      }
    };

    load().catch(() => {
      setError(`Failed to fetch delta data for "${attributeName}".`);
    });
  }, [scenarioAId, scenarioBId, attributeName, title]);

  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
      <div
        style={{
          position: "absolute",
          bottom: 24,
          left: 12,
          background: "rgba(255,255,255,0.85)",
          padding: "6px 10px",
          borderRadius: 4,
          fontSize: 11,
          lineHeight: 1.6,
        }}
      >
        <span style={{ color: "#67001f" }}>■</span> Decrease&nbsp;&nbsp;
        <span style={{ color: "#f7f7f7", border: "1px solid #aaa" }}>■</span> Unchanged&nbsp;&nbsp;
        <span style={{ color: "#053061" }}>■</span> Increase
      </div>
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

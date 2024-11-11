import { MapContainer, TileLayer, Marker } from "react-leaflet";

function Map() {
  return (
    <MapContainer
      center={[50.04028837056532, 19.97721702518615]}
      zoom={10}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png"
      />
    </MapContainer>
  );
}
export default Map;

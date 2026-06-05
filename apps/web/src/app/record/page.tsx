import RecorderForm from "@/components/RecorderForm";

export default function RecordPage() {
  return (
    <main
      style={{
        maxWidth: 640,
        margin: "0 auto",
        padding: "1.5rem",
        display: "flex",
        flexDirection: "column",
        gap: "1.5rem",
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 600 }}>Record a Story</h1>
      <RecorderForm />
    </main>
  );
}

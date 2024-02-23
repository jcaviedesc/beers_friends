const API = "http://127.0.0.1:8000";

export async function GET() {
  const res = await fetch(`${API}/beers`);
  const data = await res.json();

  return Response.json({ data });
}

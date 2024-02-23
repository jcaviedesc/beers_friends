const API = "http://127.0.0.1:8000";

export async function POST() {
  const res = await fetch(`${API}/pay`);
  const data = await res.json();

  return Response.json({ data });
}

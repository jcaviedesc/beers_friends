import { NextApiRequest } from "next";

const API = "http://127.0.0.1:8000";

export async function POST(request: Request) {
  const { orderId, friendId } = await request.json();
  console.log({ orderId, friendId });
  const res = await fetch(
    `${API}/pay?order_id=${orderId}${friendId ? `&friend_id=${friendId}` : ""}`,
    {
      method: "POST",
    }
  );
  if (res.status !== 200) {
    return new Response(`Webhook error: ${res.json()}`, {
      status: res.status,
    });
  }
  const data = await res.json();
  return Response.json({ data });
}

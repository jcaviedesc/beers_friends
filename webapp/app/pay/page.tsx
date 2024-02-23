"use client";

import { useState } from "react";
import { Textfield, Button } from "@wonderflow/react-components";

const PayBillingPage = () => {
  const [friendId, setFriendId] = useState("");
  const [paymentStatus, setPaymentStatus] = useState("");

  const handlePayment = async () => {
    try {
      const response = await fetch("/api/payments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ friendId }),
      });

      if (response.ok) {
        setPaymentStatus("Payment successful!");
      } else {
        setPaymentStatus("Payment failed!");
      }
    } catch (error) {
      console.error("Error:", error);
      setPaymentStatus("An error occurred while processing the payment.");
    }
  };

  return (
    <div>
      <h1>Pay Billing</h1>
      <Textfield
        type="text"
        value={friendId}
        onChange={(e) => setFriendId(e.target.value)}
        placeholder="Enter friend ID"
      />
      <Button onClick={handlePayment}>Pay</Button>
      {paymentStatus && <p>{paymentStatus}</p>}
    </div>
  );
};

export default PayBillingPage;

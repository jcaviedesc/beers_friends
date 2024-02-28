"use client";

import { useState } from "react";
import {
  Container,
  Textfield,
  Button,
  Card,
  Text,
  Separator,
  Spinner,
} from "@wonderflow/react-components";
import styles from "./page.module.css";

const PayBillingPage = () => {
  const [paymentStatus, setPaymentStatus] = useState("");

  const handlePayment = async (event) => {
    // Prevent the form from submitting
    event.preventDefault();
    setPaymentStatus("pending");
    // Get the friend ID and order ID from the form
    const friendId = event.target.friendId.value;
    const orderId = event.target.orderId.value;

    try {
      const response = await fetch("/api/payments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ friendId, orderId }),
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
    <div className={styles.page}>
      {paymentStatus === "pending" && <Spinner />}
      <Container dimension="extra-small" className="ContainerEx">
        <h1>Pay Billing</h1>
        <form onSubmit={handlePayment}>
          <Card>
            <div className={styles.formSection}>
              <Text
                as="label"
                htmlFor="orderId"
                variant="subtitle-2"
                color="danger"
              >
                Order ID
              </Text>
              <Textfield
                id="orderId"
                type="text"
                placeholder="Enter Order ID"
                required
              />
            </div>
            <div className={styles.formSection}>
              <Text
                as="label"
                htmlFor="friendId"
                variant="subtitle-2"
                color="danger"
              >
                Friend ID
              </Text>
              <Textfield
                id="friendId"
                type="text"
                placeholder="Enter friend ID"
              />
            </div>
            <Separator />
            <div className={styles.formSection}>
              <Button className={styles.button} type="submit">
                Pay
              </Button>
            </div>
          </Card>
        </form>
        {paymentStatus && <p>{paymentStatus}</p>}
      </Container>
    </div>
  );
};

export default PayBillingPage;

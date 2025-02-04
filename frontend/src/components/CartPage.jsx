import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import './CartPage.css'; // Add this line to import the styles

function CartPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const { tickets = {}, totalPrice = 0 } = location.state || {};

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [confirmEmail, setConfirmEmail] = useState("");
    const [mpesaNumber, setMpesaNumber] = useState("");
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const handlePayment = async (event) => {
        event.preventDefault();
        setLoading(true);
        setMessage("");

        if (email !== confirmEmail) {
            setMessage("Emails do not match!");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/mpesa/stkpush", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phone: mpesaNumber, amount: totalPrice })
            });

            const data = await response.json();
            if (data.ResponseCode === "0") {
                setMessage("Payment request sent. Enter your MPESA PIN.");
                setTimeout(() => navigate("/userProfile"), 5000);
            } else {
                setMessage("Payment request failed. Try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("Payment request failed.");
        }

        setLoading(false);
    };

    return (
        <div className="container">
            <h2>Your Cart</h2>
            <ul>
                {Object.entries(tickets)
                    .filter(([tier, count]) => count > 0)
                    .map(([tier, count]) => (
                        <li key={tier}>
                            {count} x {tier} Ticket(s)
                        </li>
                    ))}
            </ul>
            <h3>Total: KSh {totalPrice}</h3>

            <h2>Payment Information</h2>
            <form onSubmit={handlePayment}>
                <label>
                    Name:
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </label>
                <label>
                    Email:
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </label>
                <label>
                    Confirm Email:
                    <input type="email" value={confirmEmail} onChange={(e) => setConfirmEmail(e.target.value)} required />
                </label>
                <label>
                    MPESA Number:
                    <input type="text" value={mpesaNumber} onChange={(e) => setMpesaNumber(e.target.value)} required />
                </label>
                <button type="submit" disabled={loading}>
                    {loading ? "Processing..." : "Proceed to Payment"}
                </button>
            </form>

            {message && <p>{message}</p>}
        </div>
    );
}

export default CartPage;

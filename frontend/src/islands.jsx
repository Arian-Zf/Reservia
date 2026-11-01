// تنها نقطه‌ی ورود جاوااسکریپت: فقط صفحه‌ی رزرو یک «جزیره‌ی React» دارد.
import { createRoot } from "react-dom/client";
import "./styles.css";
import Booking from "./Booking.jsx";
import { setCsrf } from "./api.js";

const el = document.getElementById("booking-root");
if (el) {
  setCsrf(el.dataset.csrf || "");
  createRoot(el).render(<Booking initialService={el.dataset.service || ""} />);
}

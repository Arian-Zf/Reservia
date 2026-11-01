import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "./api.js";

const DAYS = 14;
const pad = (n) => String(n).padStart(2, "0");
const ymd = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const fa = (d, opts) => d.toLocaleDateString("fa-IR", opts);
const faTime = (iso) => new Date(iso).toLocaleTimeString("fa-IR", { hour: "2-digit", minute: "2-digit" });
const money = (n) => Number(n).toLocaleString("fa-IR");

function Step({ n, title, children }) {
  return (
    <section className="card p-6">
      <h2 className="mb-5 flex items-center gap-3 font-bold">
        <span className="step-no !h-8 !w-8 text-sm">{n.toLocaleString("fa-IR")}</span>
        {title}
      </h2>
      {children}
    </section>
  );
}

export default function Booking({ initialService }) {
  const days = useMemo(
    () =>
      Array.from({ length: DAYS }, (_, i) => {
        const d = new Date();
        d.setDate(d.getDate() + i);
        return d;
      }),
    []
  );
  const [services, setServices] = useState(null);
  const [serviceId, setServiceId] = useState("");
  const [day, setDay] = useState(ymd(days[0]));
  const [slots, setSlots] = useState([]);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [selected, setSelected] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    api("/services/")
      .then((list) => {
        setServices(list);
        const pick = list.find((s) => String(s.id) === String(initialService)) || list[0];
        if (pick) setServiceId(String(pick.id));
      })
      .catch((e) => {
        setServices([]);
        setError(e.message);
      });
  }, [initialService]);

  const loadSlots = useCallback(async () => {
    setLoadingSlots(true);
    setSelected(null);
    try {
      setSlots(await api(`/slots/?date=${day}`));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoadingSlots(false);
    }
  }, [day]);

  useEffect(() => {
    loadSlots();
  }, [loadSlots]);

  async function submit() {
    setBusy(true);
    setError("");
    try {
      await api("/appointments/", { method: "POST", body: { service: Number(serviceId), start_time: selected } });
      setDone(true);
    } catch (e) {
      setError(e.message);
      loadSlots();
    } finally {
      setBusy(false);
    }
  }

  if (done) {
    return (
      <div className="card mx-auto max-w-lg p-10 text-center">
        <p className="text-5xl">🌸</p>
        <h2 className="mt-4 text-2xl font-extrabold">نوبتت ثبت شد!</h2>
        <p className="mt-3 text-sm leading-7 text-plum-900/65">منتظر دیدنت هستیم. می‌توانی نوبتت را از بخش «نوبت‌های من» ببینی یا لغو کنی.</p>
        <a href="/my/" className="btn btn-primary mt-8">نوبت‌های من</a>
      </div>
    );
  }

  const service = services?.find((s) => String(s.id) === serviceId);
  const dayObj = days.find((d) => ymd(d) === day);

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_20rem]">
      <div className="space-y-6">
        <Step n={1} title="خدمت را انتخاب کن">
          {services === null ? (
            <div className="h-24 animate-pulse rounded-2xl bg-rose-50" />
          ) : services.length === 0 ? (
            <p className="text-sm text-plum-900/60">هنوز خدمتی تعریف نشده است.</p>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2">
              {services.map((s) => (
                <button
                  key={s.id}
                  onClick={() => setServiceId(String(s.id))}
                  className={`rounded-2xl border p-4 text-start transition ${
                    serviceId === String(s.id)
                      ? "border-rose-400 bg-rose-50 ring-4 ring-rose-100"
                      : "border-rose-100 bg-white hover:border-rose-300"
                  }`}
                >
                  <p className="font-bold">{s.name}</p>
                  {s.price_from && <p className="mt-1 text-xs text-plum-900/55">از {money(s.price_from)} تومان</p>}
                </button>
              ))}
            </div>
          )}
        </Step>

        <Step n={2} title="روز را انتخاب کن">
          <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-2">
            {days.map((d) => (
              <button
                key={ymd(d)}
                onClick={() => setDay(ymd(d))}
                className={`shrink-0 rounded-2xl border px-4 py-3 text-center transition ${
                  day === ymd(d)
                    ? "border-rose-500 bg-rose-500 text-white shadow-md shadow-rose-300/50"
                    : "border-rose-100 bg-white hover:border-rose-300"
                }`}
              >
                <span className="block text-xs opacity-80">{fa(d, { weekday: "short" })}</span>
                <span className="mt-0.5 block font-bold">{fa(d, { day: "numeric", month: "short" })}</span>
              </button>
            ))}
          </div>
        </Step>

        <Step n={3} title="ساعت را انتخاب کن">
          {loadingSlots ? (
            <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className="h-11 animate-pulse rounded-xl bg-rose-50" />
              ))}
            </div>
          ) : slots.length === 0 ? (
            <p className="text-sm text-plum-900/60">برای این روز زمان خالی وجود ندارد؛ روز دیگری را امتحان کن.</p>
          ) : (
            <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
              {slots.map((s) => (
                <button
                  key={s}
                  onClick={() => setSelected(s)}
                  className={`rounded-xl border py-2.5 text-sm transition ${
                    selected === s
                      ? "border-rose-500 bg-rose-50 font-bold text-rose-700 ring-4 ring-rose-100"
                      : "border-rose-100 bg-white hover:border-rose-300"
                  }`}
                >
                  {faTime(s)}
                </button>
              ))}
            </div>
          )}
        </Step>
      </div>

      <aside className="lg:sticky lg:top-24 lg:self-start">
        <div className="card p-6">
          <h2 className="font-bold">خلاصه‌ی نوبت</h2>
          <dl className="mt-5 space-y-4 text-sm">
            <div className="flex justify-between gap-3"><dt className="text-plum-900/55">خدمت</dt><dd className="font-medium">{service?.name || "—"}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-plum-900/55">روز</dt><dd className="font-medium">{dayObj ? fa(dayObj, { weekday: "long", day: "numeric", month: "long" }) : "—"}</dd></div>
            <div className="flex justify-between gap-3"><dt className="text-plum-900/55">ساعت</dt><dd className="font-medium">{selected ? faTime(selected) : "—"}</dd></div>
          </dl>
          {error && <p className="mt-5 rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p>}
          <button disabled={!selected || !serviceId || busy} onClick={submit} className="btn btn-primary mt-6 w-full">
            {busy ? "در حال ثبت..." : "ثبت نوبت"}
          </button>
        </div>
      </aside>
    </div>
  );
}

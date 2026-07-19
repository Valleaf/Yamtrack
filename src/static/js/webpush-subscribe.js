// Web Push (mobile/PWA) notification subscription management.
//
// Lives on the notifications settings page. Registers the service worker's
// PushManager, POSTs the resulting subscription to the server, and reflects
// enabled/disabled state in the toggle. Separate from serviceworker.js's own
// install/fetch handling -- this only deals with the push subscription
// lifecycle; the actual `push` event display logic lives in the service
// worker itself so it can fire even when this page isn't open.

function getCsrfToken() {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; i++) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

async function postSubscription(url, subscription) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(subscription.toJSON()),
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.error || "Request failed");
  }
  return response.json();
}

function initWebPushToggle() {
  const toggle = document.getElementById("id_webpush_enabled");
  const statusEl = document.getElementById("webpush-status");
  if (!toggle) return; // not rendered when WEBPUSH_ENABLED is false server-side

  const vapidPublicKey = toggle.dataset.vapidPublicKey;
  const subscribeUrl = toggle.dataset.subscribeUrl;
  const unsubscribeUrl = toggle.dataset.unsubscribeUrl;

  function setStatus(text, isError) {
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.classList.toggle("text-red-400", !!isError);
    statusEl.classList.toggle("text-gray-400", !isError);
  }

  async function getExistingSubscription() {
    const registration = await navigator.serviceWorker.ready;
    return registration.pushManager.getSubscription();
  }

  async function subscribe() {
    if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
      setStatus("Push notifications aren't supported in this browser.", true);
      toggle.checked = false;
      return;
    }

    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      setStatus("Notification permission was not granted.", true);
      toggle.checked = false;
      return;
    }

    try {
      const registration = await navigator.serviceWorker.ready;
      let subscription = await registration.pushManager.getSubscription();
      if (!subscription) {
        subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
        });
      }
      await postSubscription(subscribeUrl, subscription);
      setStatus("Push notifications enabled on this device.", false);
    } catch (err) {
      console.error("Push subscribe failed:", err);
      setStatus("Couldn't enable push notifications on this device.", true);
      toggle.checked = false;
    }
  }

  async function unsubscribe() {
    try {
      const subscription = await getExistingSubscription();
      if (subscription) {
        await postSubscription(unsubscribeUrl, subscription);
        await subscription.unsubscribe();
      }
      setStatus("Push notifications disabled on this device.", false);
    } catch (err) {
      console.error("Push unsubscribe failed:", err);
      setStatus("Couldn't disable push notifications on this device.", true);
    }
  }

  toggle.addEventListener("change", function () {
    if (toggle.checked) {
      subscribe();
    } else {
      unsubscribe();
    }
  });

  // Reflect actual current subscription state on load (in case it drifted
  // from what the server has, e.g. permission revoked in browser settings).
  if ("serviceWorker" in navigator) {
    getExistingSubscription()
      .then((subscription) => {
        toggle.checked = !!subscription;
        if (subscription) {
          setStatus("Push notifications are enabled on this device.", false);
        }
      })
      .catch(() => {});
  }
}

document.addEventListener("DOMContentLoaded", initWebPushToggle);

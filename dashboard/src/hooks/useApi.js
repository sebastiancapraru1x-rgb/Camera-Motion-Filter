import { useState, useCallback, useEffect } from 'react';

const API_BASE = '/api';

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (url, options = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}${url}`, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
      });
      if (!res.ok) throw new Error(`Request failed: ${res.status}`);
      const data = await res.json();
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { request, loading, error };
}

export function useInterval(callback, delay) {
  const savedCallback = useCallback(callback, [callback]);

  useEffect(() => {
    if (delay === null) return;
    const id = setInterval(savedCallback, delay);
    return () => clearInterval(id);
  }, [delay, savedCallback]);
}

import { config } from '../config/localconfig';

export async function api({
  method = 'GET',
  endpoint,
  data,
  rawBody = false,
}) {
  const url = `${config.apiUrl}${endpoint}`;
  const params = {
    method,
    headers: {},
    mode: 'cors',
  };

  if (!rawBody) {
    params.headers['Content-Type'] = 'application/json';
  }

  if (data) {
    params.body = rawBody ? data : JSON.stringify(data);
  }

  return fetch(url, params)
    .then(checkStatus)
    .then(
      resp =>
        resp.json().catch(error => {
          console.warn("Response from API wasn't JSON serializable", error);
          return {};
        }), // We should always return with an object)
    )
    .catch(errorHandler);
}
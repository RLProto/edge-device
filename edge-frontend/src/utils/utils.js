export const DEFAULT_URL = `${window.location.protocol}//${window.location.hostname}:8123/`;

export const $ = (element) => {
  return document.querySelector(element);
};

export const $$ = (element) => {
  return document.querySelectorAll(element);
};

export async function sendData(path, headers, data) {
  const url = DEFAULT_URL + path;
  console.log(data);
  const response = await fetch(url, {
    method: "POST",
    headers: headers,
    body: data,
  });
  return response.json();
}

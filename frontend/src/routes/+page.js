import { get } from 'svelte/store';
import { token } from "$lib/cookie.js"

export const load = async ({ fetch }) => {
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/home`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: get(token)
		}
	});

	resp = await resp.json();
	if (resp.status == 200) {
		return resp
    }
}

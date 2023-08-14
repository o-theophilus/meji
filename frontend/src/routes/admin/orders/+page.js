import { get } from 'svelte/store';
import { loading, user } from "$lib/store.js"
import { token } from "$lib/cookie.js"

export const load = async ({ fetch }) => {
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/orders`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: get(token)
		}
	});
	resp = await resp.json();
	loading.set(false)


	if (resp.status == 200) {
		return resp
    }
}

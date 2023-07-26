import { get } from 'svelte/store';
import { loading } from "$lib/store.js"
import { token } from "$lib/cookie.js"

export const load = async ({ fetch, params }) => {
	loading.set(true)
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${params.order}`, {
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

import { get } from 'svelte/store';
import { state } from "$lib/store.js"
import { token } from "$lib/cookie.js"

export const load = async ({ fetch, url }) => {
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/shop`)	
	if (url.search){	
		let temp = get(state)
		temp.shop = url.search
		state.set(temp)

		backend.search = url.search
	}

	
	let resp = await fetch(backend.href, {
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

import { get } from 'svelte/store';
import { token } from "$lib/cookie.js"

export const load = async ({ fetch, params }) => {
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item_info/${params.item}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: get(token)
		}
	});

	resp = await resp.json();

	if (resp.status == 200) {
		return {
			item: resp.item,
			group: resp.group
		}
    }
}

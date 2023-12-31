import { error } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, parent }) => {

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/advert`)
	let page_name = "adverts"

	if (url.search) {
		let temp = get(state)
		temp.shop = url.search
		state.set(temp)

		backend.search = url.search
	}

	let a = await parent();
	if (!a.locals.user.roles.includes("item:advert")) {
		throw error(400, "unauthorized access")
	}

	let resp = await fetch(backend.href, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)

	if (resp.status == 200) {
		resp.page_name = page_name
		return resp
	}
}



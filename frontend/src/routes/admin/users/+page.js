import { error } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, parent }) => {

	let page_name = "users"
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/users`)
	let temp = get(state)
	if (url.search) {
		temp[page_name] = url.search
		state.set(temp)
	}
	if (temp[page_name]) {
		backend.search = temp[page_name]
	}

	let a = await parent();
	if (!a.locals.user.permissions.includes("user:view")) {
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

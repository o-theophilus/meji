import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, params, parent }) => {

	let a = await parent();

	let page_name = "feedback"
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/feedback/${a.locals.user.key}/${params.slug}`)
	let temp = get(state)
	if (url.search) {
		temp[page_name] = url.search
		state.set(temp)
	}
	if (temp[page_name]) {
		backend.search = temp[page_name]
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

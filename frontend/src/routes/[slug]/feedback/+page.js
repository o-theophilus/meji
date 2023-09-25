import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, params, parent }) => {

	let a = await parent();

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/feedback/${a.locals.user.key}/${params.slug}`)
	if (url.search) {
		let temp = get(state)
		temp.feedback = url.search
		state.set(temp)

		backend.search = url.search
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
		return resp
	}
}

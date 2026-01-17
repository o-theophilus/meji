import { error } from '@sveltejs/kit';
import { loading, page_state } from "$lib/store.svelte.js"

export const load = async ({ fetch, url, parent }) => {
	
	let page_name = "home"
	if (!page_state.state[page_name]) {
		page_state.state[page_name] = {
			searchParams: {},
			data: [],
			loaded: false
		}
	} else if (page_state.state[page_name].loaded) {
		return page_state.state[page_name].data
	}

	let a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/home`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.close()

	if (resp.status == 200) {
		resp.page_name = page_name
		page_state.state[page_name].data = resp
		page_state.state[page_name].loaded = true

		return resp
	} else {
		throw error(resp.status, resp.error)
	}
}

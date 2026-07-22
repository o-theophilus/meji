import { loading, page_state } from "$lib/store.svelte.js";
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, url, parent }) => {

	let page_name = "home"
	if (!page_state.state[page_name]) {
		page_state.state[page_name] = {
			searchParams: {},
			data: null,
			loaded: false
		}
	} else if (page_state.state[page_name].loaded) {
		return page_state.state[page_name].data
	}

	let a = await parent();
	let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/home`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	let result = await response.json();
	loading.close()

	if (response.status == 200) {
		result.page_name = page_name
		page_state.state[page_name].data = result
		page_state.state[page_name].loaded = true

		return result
	} else {
		throw error(response.status, result.error)
	}
}

import { loading, page_state } from "$lib/store.svelte.js"
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, url, parent, depends, params }) => {
	depends(true)

	let page_name = "review"
	if (!page_state.state[page_name]) {
		let sp = {}
		for (let [key, value] of url.searchParams) {
			sp[key] = value
		}
		page_state.state[page_name] = {
			searchParams: sp,
			data: null,
			loaded: false
		}
		// } else if (page_state.state[page_name].loaded) {
		// return page_state.state[page_name].data
	}


	let backend = new URL(`${import.meta.env.VITE_BACKEND}/items/${params.slug}/comments`)
	backend.search = new URLSearchParams(page_state.state[page_name].searchParams);
	let a = await parent();
	let response = await fetch(backend.href, {
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
		throw error(result.status, result.error)
	}
}

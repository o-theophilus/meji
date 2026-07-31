import { app } from "$lib/store.svelte.js";
import { error } from '@sveltejs/kit';

export const load = async ({ fetch, params, parent, url }) => {
	if (app.item.slug == params.slug) return { item: app.item }

	let a = await parent();
	let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/${params.slug}${url.search}`, {
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		},
	});
	let result = await response.json();

	if (response.status == 200) {
		return result
	} else {
		throw error(result.status, result.error)
	}
}
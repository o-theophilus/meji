import { get } from 'svelte/store';
import { nav_portal } from "$lib/store.js"

export const load = async ({ fetch, params, parent, depends }) => {
	let temp = get(nav_portal)
	if (temp) {
		nav_portal.set(null)
		depends("")
		return {
			status: 202,
			item: temp,
			feedbacks: [],
			give_feedback: false,
			groups: []
		}
	}

	let a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${params.slug}`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});

	resp = await resp.json();

	if (resp.status == 200) {
		return resp
	}
}

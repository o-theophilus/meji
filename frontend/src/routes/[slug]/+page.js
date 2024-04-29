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
	const item = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${params.slug}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: a.locals.token
			}
		});
		resp = await resp.json();
		return resp
	}
	const group = async (item_key) => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/group/${item_key}/${a.locals.user.key}`);
		resp = await resp.json();
		return resp
	}

	let _item = await item()
	let _group = await group(_item.item.key)

	return {
		item: _item.item,
		groups: _group.groups
	}
}

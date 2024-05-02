import { get } from 'svelte/store';
import { state } from "$lib/store.js"

export const load = async ({ fetch, params, parent }) => {
	let a = await parent();
	const item = async () => {
		let _state = get(state)
		let j = _state.findIndex(x => x.name == "item");
		if (j != -1 && _state[j].data.slug == params.slug) {
			return { item: _state[j].data }
		}

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
		..._item,
		..._group
	}
}

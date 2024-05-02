import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, url, params, parent, depends }) => {

	let page_name = "feedback"
	let _state = get(state)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name,
			search: url.search
		})
		state.set(_state)
		i = _state.findIndex(x => x.name == page_name);
	}

	let a = await parent();
	const item = async () => {
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
	const feedbacks = async (item_key) => {
		let backend = new URL(`${import.meta.env.VITE_BACKEND}/feedback/${item_key}/${a.locals.user.key}`)
		backend.search = _state[i].search
		let resp = await fetch(backend.href);
		resp = await resp.json();
		return resp
	}
	let _item = await item()
	let _feedbacks = await feedbacks(_item.item.key)
	loading.set(false)

	return {
		page_name: page_name,
		..._item,
		..._feedbacks
	}
}
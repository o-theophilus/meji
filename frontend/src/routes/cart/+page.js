import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, parent }) => {

	let page_name = "cart"
	let _state = get(state)
	let i = _state.findIndex(x => x.name == page_name);

	if (i == -1) {
		_state.push({
			name: page_name,
			data: [],
			loaded: false
		})
		state.set(_state)
		i = _state.findIndex(x => x.name == page_name);
	} else if (_state[i].loaded) {
		return _state[i].data
	}

	let a = await parent();
	let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json',
			Authorization: a.locals.token
		}
	});
	resp = await resp.json();
	loading.set(false)

	if (resp.status == 200) {
		_state[i].data = resp
		_state[i].loaded = true
		state.set(_state)

		return resp
	}
}

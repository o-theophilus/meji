import { get } from 'svelte/store';
import { state, loading } from "$lib/store.js"

export const load = async ({ fetch, parent }) => {

	let page_name = "home"
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
	
	loading.set(true)
	let a = await parent();
	const new_arrivals = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/shop?order=latest&page_size=8`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: a.locals.token
			}
		});
		resp = await resp.json();
		return resp
	}
	const offers = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/shop?order=discount&page_size=8`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: a.locals.token
			}
		});
		resp = await resp.json();
		return resp
	}


	let _new_arrivals = await new_arrivals()
	let _offers = await offers()

	let data = {
		new_arrivals: _new_arrivals.items,
		offers: _offers.items
	}

	_state[i].data = data
	_state[i].loaded = true

	loading.set(false)
	return data
}

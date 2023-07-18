import { writable, get } from 'svelte/store';
import { page } from '$app/stores';
import { invalidate } from '$app/navigation';

export const _tick = writable("");
export const tick = (data)=> {
	_tick.set(data);
}

export const module = writable();
export const loading = writable(false);
export const user = writable();
export const portal = writable();

export const state = writable({})
export const set_state = (page_name, key, value) => {
    let _page = get(page);
    _page.url.searchParams.set(key, value);

    if (value == '') {
        _page.url.searchParams.delete(key);
    }
    if (['tag', 'search', "status"].includes(key)) {
        _page.url.searchParams.delete("page_no");
    }

    window.history.pushState(history.state, '', _page.url.href);

    let temp = get(state)
    temp[page_name] = _page.url.search
    state.set(temp)
    loading.set(true)
    
    invalidate(() => true);
};

export const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export const months = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

export const ordinal_suffix_of = (i) => {
	var j = i % 10,
		k = i % 100;
		if (j == 1 && k != 11) {
		return i + 'st';
	}
	if (j == 2 && k != 12) {
		return i + 'nd';
	}
	if (j == 3 && k != 13) {
		return i + 'rd';
	}
	return i + 'th';
};



export const save_queue = writable([]);
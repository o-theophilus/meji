import { writable, get } from 'svelte/store';
import { page } from '$app/stores';
import { invalidate } from '$app/navigation';

export const state = writable({})
export const set_state = (pn, key, value) => {
    let _page = get(page);
    _page.url.searchParams.set(key, value);

    if (key == 'tag' && value == 'all') {
        value = '';
    }
    if (value == '') {
        _page.url.searchParams.delete(key);
    }

    window.history.pushState(history.state, '', _page.url.href);

    let temp = get(state)
    temp[pn] = _page.url.search
    state.set(temp)
    
    invalidate(() => true);
};



export const page_name = writable("")


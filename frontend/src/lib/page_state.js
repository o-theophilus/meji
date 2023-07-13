import { writable, get } from 'svelte/store';

let default_page = {
	search: '',
	tag: '',
	status: '',
	page_no: 1,
	order: ['date', 'dsc']
};
export const state = writable({
		shop: {...default_page, status: "live"},
		save: { ...default_page },
		users: { ...default_page, status: "confirm"},
		ad: { ...default_page },
		orders: {...default_page, status: "ordered"}
	}
)

export const page_name = writable();
// export const get_query = (name) => {
// 	page_name.set(name);
// 	let query = '';
// 	let page = get(state)[name]
	
// 	query += `&page_no=${page.page_no}`;
// 	query += `&order=${page.order}`;

// 	if (page.search) {
// 		query += `&search=${page.search}`;
// 	}
// 	if (page.tag) {
// 		query += `&tag=${page.tag}`;
// 	}
// 	if (page.status) {
// 		query += `&status=${page.status}`;
// 	}

	
// 	if (query) {
// 		query = `?${query.substring(1)}`;
// 	}
	
// 	return query;
// };

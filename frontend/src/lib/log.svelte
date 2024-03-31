<script>
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { token } from '$lib/cookie.js';

	export let action = null;
	export let entity_key = null;
	export let entity_type = null;
	export let status = 200;
	export let misc = {};

	$: if (action == 'goto') {
		entity_key = `${$page.url.pathname}${$page.url.search}`;
		entity_type = 'location';
	}

	let prev;
	$: if (prev != entity_key && browser) {
		prev = entity_key;

		fetch(`${import.meta.env.VITE_BACKEND}/log`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				action,
				entity_key,
				entity_type,
				status,
				misc
			})
		});
	}
</script>

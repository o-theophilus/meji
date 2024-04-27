<script>
	import { state } from '$lib/store.js';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	console.log($page.data.page_name);

	onMount(() => {
		// TODO: components should get the page name directly
		let i = $state.findIndex((x) => x.name == $page.data.page_name);

		if (i != -1) {
			for (const x of new URLSearchParams($state[i].search)) {
				$page.url.searchParams.set(x[0], x[1]);
			}
			window.history.replaceState(history.state, '', $page.url.href);
		}
	});
</script>

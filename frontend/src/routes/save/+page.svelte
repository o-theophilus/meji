<script>
	import { flip } from 'svelte/animate';
	import { backInOut } from 'svelte/easing';

	import { user } from '$lib/store.js';
	import { state, page_name } from '$lib/page_state.js';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body_item.svelte';
	import Item from '$lib/comp/item.svelte';
	import Pagination from '$lib/comp/pagination.svelte';

	export let user = { saves: [] };
	$: user = $user ? $user : user;

	$page_name = 'save';
	let size = 24;
	$: start = ($state[$page_name].page_no - 1) * size;
	$: total_page = Math.ceil(user.saves.length / size);
	$: items = user.saves.slice(start, start + size);
</script>

<svelte:head>
	<title>Saved | Meji</title>
</svelte:head>

<Card>
	<Title title="Saved" />
	<Body grid>
		{#each items as item (item.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: backInOut }}>
				<Item {item} />
			</div>
		{:else}
			no saved item
		{/each}
	</Body>
	<Pagination {total_page} />
</Card>

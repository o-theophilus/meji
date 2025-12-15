<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';

	import { app } from '$lib/store.svelte.js';
	import { Content } from '$lib/layout';
	import { PageNote } from '$lib/info';
	import { Meta, Icon, Log } from '$lib/macro';

	import Item from './item.svelte';
	import Checkout from './checkout.svelte';

	// let { data } = $props();
	// let items = $state(data.items);
	// let cart = data.cart;

	// const update = (a) => {
	// 	items = a;
	// };
</script>

<Log entity_type={'page'} />
<Meta
	title="Save"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

<Content --content-padding-top="1px" --content-background-color="var(--bg2)">
	<div class="page_title">Cart</div>

	{#if app.cart_items.length}
		{#each app.cart_items as item (item.key + JSON.stringify(item.variation))}
			<div animate:flip={{ delay: 0, duration: 500, easing: cubicInOut }}>
				<Item {item} />
			</div>
		{/each}
	{:else}
		<PageNote>
			<Icon icon="search" size="50" />
			No item found
		</PageNote>
	{/if}
</Content>

<Checkout></Checkout>

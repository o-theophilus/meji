<script>
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { onMount } from 'svelte';

	import { app, module } from '$lib/store.svelte.js';
	import { Content } from '$lib/layout';
	import { PageNote } from '$lib/info';
	import { Button } from '$lib/button';
	import { Icon } from '$lib/macro';
	import { Login } from '$lib/auth';

	import Item from './item.svelte';
	import Next from '../next.svelte';

	let { ops = $bindable() } = $props();

	let total = $derived.by(() => {
		let temp = 0;
		for (const i of app.cart_items) {
			temp += i.price * i.quantity;
		}
		return temp;
	});
</script>

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
			No item in cart yet
			<div class="icon">
				<Icon icon="cart" size="50" />
			</div>
			<Button href="/shop">Shop now</Button>
		</PageNote>
	{/if}
</Content>

{#if app.cart_items.length}
	<Next
		value={total}
		label="Total Amount"
		btn_label="{!app.login ? 'Login to ' : ''}Checkout"
		icon="cart"
		onclick={() => {
			if (app.login) {
				ops.status = 'receiver';
			} else {
				module.open(Login);
			}
		}}
	></Next>
{/if}

<style>
	.page_title {
		margin: 24px 0;
	}
	.icon {
		fill: var(--ft2);
	}
</style>

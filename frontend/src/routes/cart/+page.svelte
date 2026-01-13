<script>
	import { app } from '$lib/store.svelte.js';
	import { Meta, Log } from '$lib/macro';

	import Cart from './1_cart/index.svelte';
	import Receiver from './2_receiver/index.svelte';
	import Pay from './3_pay/index.svelte';
	import { onMount } from 'svelte';

	let { data } = $props();
	// let cart = data.cart;
	onMount(() => {
		app.cart_items = data.items;
	});

	let ops = $state({
		status: 'cart',
		cart: data.cart,
		isFilled() {
			return !!(
				this.cart.receiver?.name &&
				this.cart.receiver?.phone &&
				this.cart.receiver?.email &&
				this.cart.receiver?.address?.address &&
				this.cart.receiver?.address?.state &&
				this.cart.receiver?.address?.country
			);
		}
	});
</script>

<Log entity_type={'page'} />
<Meta
	title="Save"
	description="This page showcases a collection of interesting blogs and projects that I have worked on"
/>

{#if ops.status == 'cart'}
	<Cart bind:ops></Cart>
{:else if ops.status == 'receiver'}
	<Receiver bind:ops></Receiver>
{:else if ops.status == 'pay'}
	<Pay bind:ops></Pay>
{/if}

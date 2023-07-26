<script>
	import { user, module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Meta from '$lib/meta.svelte';
	import Eta from './eta.svelte';
	import Address from './order_address.svelte';
	import Button from '$lib/button.svelte';
	import Form from './_address.svelte';

	import Breakdown from './breakdown.svelte';
	import Action from './action.svelte';
	import Status from './status.svelte';

	import Items from './order_items.svelte';

	export let data;
	let { order } = data;
	let { previous_recipients } = data;
</script>

<Meta title="Order" description="Order" />

<Card>
	<b>
		Order ID: {order.key}
	</b>
	<section>
		<div class="block">
			{#if order.status != 'delivered'}
				<Eta {order} />
			{/if}
			<Address {order} let:complete_address>
				{#if order.status == 'pending'}
					<Button
						class={!complete_address ? 'primary' : ''}
						icon="edit"
						on:click={() => {
							$module = {
								module: Form,
								data: {
									order,
									previous_recipients
								}
							};
						}}
					/>
				{/if}
			</Address>
		</div>
		<div class="block">
			{#if order.status == 'pending'}
				<Breakdown user={$user} {order} />
				<Action {order} />
			{:else}
				<Items {order} />
				<Status {order} />
			{/if}
		</div>
	</section>
</Card>

<style>
	section,
	.block {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		width: 100%;
	}
	section {
		margin-top: var(--sp2);
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
	}
</style>

<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import Eta from '../orders/[order]/eta.svelte';
	import Receiver from '../orders/[order]/receiver.svelte';
	import Form from './delivery._receiver_form.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let cart;
	export let previous_receivers = [];

	$: complete_address =
		cart.receiver.name &&
		cart.receiver.phone &&
		cart.receiver.address.line &&
		cart.receiver.address.state &&
		cart.receiver.address.country &&
		cart.receiver.address.local_area &&
		cart.receiver.address.postal_code;
</script>

<Card>
	<div class="ctitle">
		<div class="ctitle">
			<Button
				class="round"
				on:click={() => {
					emit('back');
				}}
			>
				<SVG type="angle" size="10" />
			</Button>Delivery
		</div>
	</div>

	<br />
	<br />

	<Receiver order={cart}>
		<Button
			class="link"
			on:click={() => {
				$module = {
					module: Form,
					cart,
					previous_receivers
				};
			}}
		>
			Edit
		</Button>
	</Receiver>

	<br />

	<Eta order={cart} />

	<br />

	<span class="bold">Delivery fee:</span>
	₦{cart.transaction.delivery_fee.toLocaleString()}

	<br />
	<br />

	<Button
		class="primary"
		disabled={!complete_address}
		on:click={() => {
			emit('next');
		}}
	>
		Next
	</Button>
</Card>

<style>
	.bold {
		font-weight: 500;
		color: var(--ac1);
	}
</style>

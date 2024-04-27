<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import SVG from '$lib/svg.svelte';

	import Datetime from '$lib/datetime.svelte';
	import Receiver from './delivery.receiver.svelte';
	import Form from './delivery._receiver_form.svelte';
	import { createEventDispatcher } from 'svelte';

	let emit = createEventDispatcher();

	export let cart;
	export let prev;

	$: complete_address =
		cart.name &&
		cart.phone &&
		cart.line &&
		cart.state &&
		cart.country &&
		cart.local_area &&
		cart.postal_code;
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
					prev
				};
			}}
		>
			Edit
		</Button>
	</Receiver>

	<br />

	<span class="bold"> Estimated time of delivery: </span>
	<br />
	To be delivered on or before
	<Datetime datetime={cart.delivery_date} type="day" />,
	<Datetime datetime={cart.delivery_date} type="date" style="a" />. Time:
	<Datetime datetime={cart.delivery_date} type="time" />.

	<br />
	<br />

	<span class="bold">Delivery fee:</span>
	₦{cart.cost_delivery.toLocaleString()}

	<br />
	<br />

	<Button
		class="primary"
		disabled={!complete_address}
		on:click={() => {
			emit('next');
		}}
	>
		Place Order
	</Button>
</Card>

<style>
	.bold {
		font-weight: 700;
		color: var(--ac1);
	}
</style>

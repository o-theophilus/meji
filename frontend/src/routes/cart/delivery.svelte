<script>
	import { module } from '$lib/store.js';
	import { createEventDispatcher } from 'svelte';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button/button.svelte';
	import Link from '$lib/button/link.svelte';
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';
	import Title from '$lib/title.svelte';

	import Datetime from '$lib/datetime.svelte';
	import Receiver from './delivery.receiver.svelte';
	import Form from './delivery._receiver_form.svelte';

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
	<Title card>
		<svelte:fragment slot="left">
			<BRound
				on:click={() => {
					emit('back');
				}}
			>
				<SVG type="angle" size="10" />
			</BRound>
		</svelte:fragment>
		Delivery
	</Title>

	<br />

	<Receiver order={cart}>
		<Link
			on:click={() => {
				$module = {
					module: Form,
					cart,
					prev
				};
			}}
		>
			Edit
		</Link>
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
		primary
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

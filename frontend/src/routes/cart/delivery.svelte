<script>
	import { module } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Eta from '../orders/[order]/eta.svelte';
	import Reviever from '../orders/[order]/receiver.svelte';
	import Form from './delivery._receiver_form.svelte';

	export let cart;
	export let previous_receivers = [];
</script>

<Card>
	<Reviever order={cart}>
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
	</Reviever>
	<br />
	<Eta order={cart} />
</Card>

<style>
</style>

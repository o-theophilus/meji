<script>
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';
	import Receiver from '../../orders/[slug]/_page.receiver.svelte';

	let error = $state({});

	const submit = async (form) => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			notify.open('Receiver Information Saved');
			module.value.ops.cart = resp.cart;
			page_state.set_data('cart', resp);
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Previous Receivers" error={error.error}>
	{#each module.value.previous_receivers as receiver}
		<div class="one">
			<Receiver {receiver}>
				{#snippet top_right()}
					<Button
						--button-font-size="0.8rem"
						--button-height="32px"
						--button-outline-color-hover="var(--ol)"
						onclick={() => {
							submit({
								name: receiver.name,
								phone: receiver.phone,
								email: receiver.email,
								address: receiver.address.address,
								area: receiver.address.area,
								state: receiver.address.state,
								country: receiver.address.country
							});
						}}
					>
						Select
					</Button>
				{/snippet}
			</Receiver>
		</div>
	{/each}
</Form>

<style>
	.one {
		margin-top: 8px;
		background-color: var(--bg3);
		outline: 1px solid var(--ol);
		outline-offset: -1px;
		padding: 16px;
		border-radius: 8px;
	}
</style>

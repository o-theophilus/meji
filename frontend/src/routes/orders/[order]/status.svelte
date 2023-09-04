<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
	import Email_Processing from './email_template_processing.svelte';
	import Email_Delivered from './email_template_delivered.svelte';
	let email_template;

	export let order;
	let error = {};

	const submit = async (status = 'next') => {
		error = {};

		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_status/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				status,
				email_template: email_template.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.order;

			$module = {
				module: Info,
				status: 200,
				title: 'Status Changed',
				message: `Order status has been changed succcessfully`,
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<div class="horizontal">
	<Button
		name="<<"
		class="link"
		on:click={() => {
			submit('prev');
		}}
	/>

	{order.status}

	<Button
		name=">>"
		class="link"
		on:click={() => {
			submit('next');
		}}
	/>
</div>
<br />
{#if error.error}
	<p class="error">
		{error.error}
	</p>
	<br />
{/if}

<div bind:this={email_template} style="display: none;">
	{#if order.status == 'ordered'}
		<Email_Processing {order} />
	{:else}
		<Email_Delivered {order} />
	{/if}
</div>

<style>
	.horizontal {
		display: flex;
		gap: var(--sp1);
	}
</style>

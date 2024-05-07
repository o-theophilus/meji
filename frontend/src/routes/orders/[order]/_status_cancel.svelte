<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';
	import SVG from '$lib/svg.svelte';
	import Info from '$lib/info.svelte';

	import Email_Admin from './email_template_cancel_admin.svelte';
	import Email_User from './email_template_cancel_user.svelte';
	let email_template_admin;
	let email_template_user;

	let order = { ...$module.order };
	let items = { ...$module.items };

	let note = '';
	let error = {};

	const validate = async () => {
		error = {};

		if (!note) {
			error.note = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		$loading = 'canceling . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order_status_cancel/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				note,
				email_template_admin: email_template_admin.innerHTML.replace(/&amp;/g, '&'),
				email_template_user: email_template_user.innerHTML.replace(/&amp;/g, '&')
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'order',
				data: resp.order
			};

			$module = {
				module: Info,
				status: 200,
				title: 'Order Canceled',
				message: 'Order has been Canceled',
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

<Form>
	<svelte:fragment slot="title">
		<b>Cancel Order </b>
	</svelte:fragment>

	<IG
		name="note"
		label="Please give reason"
		{error}
		type="textarea"
		bind:value={note}
		placeholder="Reason"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button extra="hover_red" on:click={validate}>
		<SVG icon="close" size="8" />
		Cancel
	</Button>
</Form>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin {order} {items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User {order} {items} />
</div>

<style>
</style>

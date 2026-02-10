<script>
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import Email_Admin from './email/cancel_admin.svelte';
	import Email_User from './email/cancel_user.svelte';
	let email_template_admin;
	let email_template_user;

	let form = $state({ comment: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		form.email_template_admin = email_template_admin.innerHTML.replace(/&amp;/g, '&');
		form.email_template_user = email_template_user.innerHTML.replace(/&amp;/g, '&');

		loading.open('Canceling Order . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/order/cancel/${module.value.order.key}`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.order);
			notify.open('Order Canceled');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Cancel Order" error={error.error}>
	<Note status="201" note="Are you sure you want to cancel this order?"
		>Please give reason why you are canceling this order</Note
	>
	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button
			icon="trash-2"
			onclick={validate}
			--button-background-color="darkred"
			--button-background-color-hover="red"
			--button-color-hover="white">Cancel Order</Button
		>
	</div>
</Form>

<div bind:this={email_template_admin} style="display: none;">
	<Email_Admin order={module.value.order} items={module.value.items} />
</div>
<div bind:this={email_template_user} style="display: none;">
	<Email_User order={module.value.order} items={module.value.items} />
</div>

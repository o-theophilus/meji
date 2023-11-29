<script>
	import { page } from '$app/stores';

	import Template from '$lib/email_template.svelte';
	import Items from './email_template__items.svelte';

	export let order;
</script>

<Template>
	Dear {'{'}user_name{'}'}
	<br />
	<br />
	Your order:
	<a
		style="
text-decoration: none;
color: #1d9bf0;
"
		href="{$page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key}
	</a>
	has been canceled.

	<br />
	<br />
	<Items {order} />
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>

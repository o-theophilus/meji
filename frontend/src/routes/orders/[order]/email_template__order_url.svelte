<script>
	import { page } from '$app/stores';

	export let order;
</script>

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
